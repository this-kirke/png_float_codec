#!/usr/bin/python

import filecmp;
import math;
import numpy;
from PIL import Image;
import struct;
import sys;

def float_array_to_rgba_buffer( float_array ):
	bit_shift = numpy.array( [ math.pow( 256, 3), math.pow( 256, 2), math.pow( 256, 1), math.pow( 256, 0 ) ] );
	bit_mask = numpy.array( [0.0, 1.0 / 256.0, 1.0 / 256.0, 1.0 / 256.0] );

	rgba_buffer = numpy.empty( ( float_array.shape[0], float_array.shape[1], 4 ) );

	for row in range( float_array.shape[0] ):
		for column in range( float_array.shape[1] ):
			rgba_buffer[row][column][0] = math.modf( float_array[row][column] * bit_shift.item(0) )[0];

			rgba_buffer[row][column][1] = math.modf( float_array[row][column] * bit_shift.item(1) )[0];
			rgba_buffer[row][column][1] -= rgba_buffer[row][column][0] * bit_mask.item(1);

			rgba_buffer[row][column][2] = math.modf( float_array[row][column] * bit_shift.item(2) )[0];
			rgba_buffer[row][column][2] -= rgba_buffer[row][column][1] * bit_mask.item(2);

			rgba_buffer[row][column][3] = math.modf( float_array[row][column] * bit_shift.item(3) )[0];
			rgba_buffer[row][column][3] -= rgba_buffer[row][column][2] * bit_mask.item(3);

	return rgba_buffer;

def rgba_buffer_to_float_array( rgba_buffer ):
	bit_shift = numpy.array( [ 1.0 / math.pow( 256, 3 ), 1.0 / math.pow( 256, 2 ), 1.0 / math.pow( 256, 1 ), 1.0 / math.pow( 256, 0 ) ] );

	float_array = numpy.empty( (rgba_buffer.shape[0], rgba_buffer.shape[1] ) );
	for row in range( float_array.shape[0] ):
		for column in range( float_array.shape[1] ):
			float_array[row][column] = numpy.dot( bit_shift, rgba_buffer[row][column]);

	return float_array;

def generate_float_array( width, height ):
	float_array = numpy.empty( ( height, width ) );
	max_distance = math.sqrt( math.pow( height / 2, 2 ) + math.pow( width / 2, 2 ) );

	for row in range( height ):
		for column in range( width ):
			distance_from_center = math.sqrt( 
				math.pow( row - ( height / 2 ), 2 ) + 
				math.pow( column - ( width / 2 ), 2 )
			);

			float_array[row][column] = distance_from_center / max_distance;

			# Packing floats into 8-bit unsigned integers only works for floats in range [0, 1); 8-bit unisgned integers have a max value of 255, *not* 256
			float_array[row][column] = min( float_array[row][column], 0.9999999999999999 );

	return float_array;

def read_float_array( file_name ):
	file = open( file_name, "rb" );

	if( not file.closed ):
		width = struct.unpack( 'i', file.read( 4 ) )[0];
		height = struct.unpack( 'i', file.read( 4 ) )[0];
		
		float_array = numpy.empty( ( height, width ) );

		for row in range( height ):
			for column in range( width ):
				float_array[row][column] = struct.unpack( 'f', file.read( 4 ) )[0];
	
				# Packing floats into 8-bit unsigned integers only works for floats in range [0, 1); 8-bit unisgned integers have a max value of 255, *not* 256
				float_array[row][column] = min( float_array[row][column], 0.9999999999999999 );

	return float_array;

def write_float_array( file_name, float_array ):
	file = open( file_name, "wb" );

	if( not file.closed ):
		# Write simple header for array dimensions

		# Width
		file.write( struct.pack( 'i', float_array.shape[1] ) );

		# Height
		file.write( struct.pack( 'i', float_array.shape[0] ) );

		for value in numpy.nditer( float_array ):
			file.write( struct.pack( 'f', value ) );

		file.close();

def print_float_array( float_array ):
	for row in range( float_array.shape[0] ):
		for column in range( float_array.shape[1] ):
			print( "%.2f" % float_array[row][column] ),;
		print("");
	print("");

def print_rgba_buffer( rgba_buffer ):
	for row in range( rgba_buffer.shape[0] ):
		for column in range( rgba_buffer.shape[1] ):
			print( "( " + str( rgba_buffer[row][column][0] ) + ", " + str( rgba_buffer[row][column][1] ) + ", " + str( rgba_buffer[row][column][2] ) + ", " + str( rgba_buffer[row][column][3] ) + ")" ),;

def rgba_buffer_to_image( rgba_buffer ):
	pil_image = numpy.reshape( rgba_buffer.shape[2] * rgba_buffer.shape[1], rgba_buffer.shape[0] );
	return Image.fromarray( rgba_buffer, 'RGBA' );

def image_to_rgba_buffer( pil_image ):
	return numpy.array( pil_image.getdata(), numpy.uint8 ).reshape( pil_image.size[1], pil_image.size[0], 4 ) / 255.0 ;

def read_png_image( file_name ):
	return Image.open( file_name );

def write_png_image( file_name, pil_image ):
	pil_image.save( file_name );

def main():
	width = 7;
	height = 5;

	float_array_1 = generate_float_array( width, height );
	print_float_array( float_array_1 );
	write_float_array( "float_array_1.bin", float_array_1 );

	float_array_2 = read_float_array( "float_array_1.bin" );
	print_float_array( float_array_2 );
	write_float_array( "float_array_2.bin", float_array_2 );
	
	rgba_buffer = float_array_to_rgba_buffer( float_array_2 );
	float_array_3 = rgba_buffer_to_float_array( rgba_buffer );
	print_float_array( float_array_3 );
	write_float_array( "float_array_3.bin", float_array_3 );

	#TODO: Some precision error, or possibly some math error.  Need to verify.
	print( "float_array_1 ~ float_array_2:  " + str( numpy.allclose( float_array_1, float_array_2, .0002 ) ) );
	print( "float_array_1 ~ float_array_3:  " + str( numpy.allclose( float_array_1, float_array_3, .0002 ) ) );
	print( "float_array_2 ~ float_array_3:  " + str( numpy.allclose( float_array_2, float_array_3, .0002 ) ) );

	print( "FileCMP:  float_array_1.bin == float_array_2.bin:  " + str( filecmp.cmp( "float_array_1.bin", "float_array_2.bin" ) ) );
	print( "FileCMP:  float_array_1.bin == float_array_3.bin:  " + str( filecmp.cmp( "float_array_1.bin", "float_array_3.bin" ) ) );
	print( "FileCMP:  float_array_2.bin == float_array_3.bin:  " + str( filecmp.cmp( "float_array_2.bin", "float_array_3.bin" ) ) );
	print( "Have a nice day!  :)" );

if __name__ == "__main__":
	main();
