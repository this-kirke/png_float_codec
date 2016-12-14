#!/usr/bin/python

import filecmp;
import math;
import numpy;
import random;
import struct;
import time;

def float_array_to_rgba_buffer( float_array ):
	rgba_buffer = numpy.empty( ( float_array.shape[0], float_array.shape[1], 4 ) );

	for row in range( float_array.shape[0] ):
		for column in range( float_array.shape[1] ):
			f = abs( float_array[row][column] );
			sign = 0.0 if float_array[row][column] > 0.0 else 1.0;
			exponent = math.floor( math.log( f, 2.0 ) );
			mantissa = math.pow( 2.0, - exponent ) * f;
			
			print( "Float:  " + str( float_array[row][column] ) );
			print( "Sign:  " + str( sign) );
			print( "Exponent:  " + str( exponent ) );
			print( "Mantissa:  " + str( mantissa ) );

			exponent = math.floor( math.log( f, 2.0 ) + 127.0 ) + math.floor( math.log( mantissa, 2.0 ) );

			rgba_buffer[row][column][0] = 128.0 * sign + math.floor( exponent * math.pow( 2, -1.0 ) );
			rgba_buffer[row][column][1] = 128.0 * ( exponent % 2.0 ) + math.floor( mantissa * 128.0 ) % 128.0;
			rgba_buffer[row][column][2] = math.floor( math.floor( mantissa * math.pow( 2, 15.0) ) % math.pow( 2, 8.0 ) );
			rgba_buffer[row][column][3] = math.floor( math.pow( 2, 23.0 ) * ( mantissa % math.pow( 2, -15.0 ) ) );

	return rgba_buffer;

def rgba_buffer_to_float_array( rgba_buffer ):
	float_array = numpy.empty( (rgba_buffer.shape[0], rgba_buffer.shape[1] ) );

	for row in range( float_array.shape[0] ):
		for column in range( float_array.shape[1] ):
			sign = 1.0 - ( 0.0 if rgba_buffer[row][column][0] < 128.0 else 1.0 ) * 2.0;
			exponent = 2.0 * ( rgba_buffer[row][column][0] % 128.0 ) + ( 0.0 if rgba_buffer[row][column][1] < 128.0 else 1.0 ) - 127.0;
			mantissa = 1.0 + ( ( rgba_buffer[row][column][1] % 128.0 ) * math.pow( 2.0, 16.0 ) + rgba_buffer[row][column][2] * math.pow( 2.0, 8.0 ) + rgba_buffer[row][column][3] + 23.0 ) * math.pow( 2.0, -23.0 );

			print( "Float:  " + str( float_array[row][column] ) );
			print( "Sign:  " + str( sign) );
			print( "Exponent:  " + str( exponent ) );
			print( "Mantissa:  " + str( mantissa ) );

			float_array[row][column] = sign * math.pow( 2.0, exponent ) * mantissa;

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

	return float_array;

def generate_float_array1( width, height ):
	float_array = numpy.empty( ( height, width ) );
	max_distance = math.sqrt( math.pow( height / 2, 2 ) + math.pow( width / 2, 2 ) );

	for row in range( height ):
		for column in range( width ):
			float_array[row][column] = random.uniform( -25.0, 25.0 );

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
		print;
	print;

def print_rgba_buffer( rgba_buffer ):
	for row in range( rgba_buffer.shape[0] ):
		for column in range( rgba_buffer.shape[1] ):
			print( "( " + "%.2f" % rgba_buffer[row][column][0] + ", " + "%.2f" % rgba_buffer[row][column][1] + ", " + "%.2f" % rgba_buffer[row][column][2] + ", " "%.2f" % rgba_buffer[row][column][3] + ")" ),;
		print;
	print;

def main():
	width = 7;
	height = 5;

	float_array_1 = generate_float_array1( width, height );
	print_float_array( float_array_1 );
	write_float_array( "float_array_1.bin", float_array_1 );

	float_array_2 = read_float_array( "float_array_1.bin" );
	print_float_array( float_array_2 );
	write_float_array( "float_array_2.bin", float_array_2 );
	
	rgba_buffer = float_array_to_rgba_buffer( float_array_2 );
	print_rgba_buffer( rgba_buffer );

	float_array_3 = rgba_buffer_to_float_array( rgba_buffer );
	print_float_array( float_array_3 );
	write_float_array( "float_array_3.bin", float_array_3 );

	#TODO: Some precision error, or possibly some math error.  Need to verify.
	print( "float_array_1 ~ float_array_2:  " + str( numpy.allclose( float_array_1, float_array_2, .0002 ) ) );
	print( "float_array_1 ~ float_array_3:  " + str( numpy.allclose( float_array_1, float_array_3, .0002 ) ) );
	print( "float_array_2 ~ float_array_3:  " + str( numpy.allclose( float_array_2, float_array_3, .0002 ) ) );
	print("");
	print( "Have a nice day!  :)" );

if __name__ == "__main__":
	main();
