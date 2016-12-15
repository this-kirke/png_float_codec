#!/usr/bin/python

import numpy;
from PIL import Image;
import random;
import struct;

def generate_float_array( width, height ):
	float_array = numpy.ndarray( ( height, width ) );

	for row in range( height ):
		for column in range( width ):
			float_array[row][column] = random.uniform( -25.0, 25.0 );

	return float_array;

def float_array_to_rgba_buffer( float_array ):
	rgba_buffer = numpy.asarray( 
		struct.unpack( 
			'!%sB' % ( 4 * float_array.size ),
			struct.pack( 
				'!%sf' % float_array.size,
				*float_array.flat
			)
		)
	);

	rgba_buffer = rgba_buffer.reshape( (float_array.shape[0], float_array.shape[1], 4 ) );

	return rgba_buffer;

def rgba_buffer_to_float_array( rgba_buffer ):
	float_array = numpy.asarray(
		struct.unpack( 
			'!%sf' % ( rgba_buffer.size / 4 ), 
			struct.pack( 
				'!%sB' % rgba_buffer.size, 
				*rgba_buffer.flat
			)
		)
	);

	float_array = float_array.reshape( rgba_buffer.shape[0], rgba_buffer.shape[1] );

	return float_array;

def write_png( file_name, rgba_buffer ):
	image = Image.fromarray( numpy.uint8( rgba_buffer ) );
	image.save( file_name, "PNG" );

def read_png( file_name ):
	image = Image.open( file_name );
	rgba_buffer = numpy.asarray( image );
	return rgba_buffer;

# Printing functions
def print_float_array( float_array ):
	print( "Printing Float Array:");
	for row in range( float_array.shape[0] ):
		for column in range( float_array.shape[1] ):
			print( "%.2f" % float_array[row][column] ),;
		print("");
	print("");

def print_rgba_buffer( rgba_buffer ):
	print("Printing RGBA Buffer:");
	for row in range( rgba_buffer.shape[0] ):
		for column in range( rgba_buffer.shape[1] ):
			print( "( " + "%.2f" % rgba_buffer[row][column][0] + ", " + "%.2f" % rgba_buffer[row][column][1] + ", " + "%.2f" % rgba_buffer[row][column][2] + ", " "%.2f" % rgba_buffer[row][column][3] + ")" ),;
		print("");
	print("");

def main():
	'''
	 Float array to RGBA buffer conversion:

	 1.  Create float array.
	 2.  Convert float array to RGBA buffer.
	 3.  Convert RGBA buffer back to float array.
	 4.  Compare original float array to converted float array.

	 '''

	width = 7;
	height = 5;

	float_array_1 = generate_float_array( width, height );
	print_float_array( float_array_1 );

	rgba_buffer_1 = float_array_to_rgba_buffer( float_array_1 );
	print_rgba_buffer( rgba_buffer_1 );

	float_array_2 = rgba_buffer_to_float_array( rgba_buffer_1 );
	print_float_array( float_array_2 );

	# Testing standard floats
	print( "float_array_1 ~ float_array_2:");
	print( numpy.isclose( float_array_1, float_array_2 ) );
	print("");

	float_array_3 = generate_float_array( width, height );
	float_array_3[0][0] = float( '-inf' );
	rgba_buffer_2 = float_array_to_rgba_buffer( float_array_3 );
	float_array_4 = rgba_buffer_to_float_array( rgba_buffer_2 );

	# Testing float( 'inf' ):
	print( "float_array_3 ~ float_array_4:" );
	print( numpy.isclose( float_array_3, float_array_4 ) );
	print("");

	float_array_5 = generate_float_array( width, height );
	float_array_5[0][0] = float( '-nan' );
	rgba_buffer_3 = float_array_to_rgba_buffer( float_array_5 );
	float_array_6 = rgba_buffer_to_float_array( rgba_buffer_3 );

	# Testing float( 'nan' ):
	print( "float_array_5 ~ float_array_6:");
	print( numpy.isclose( float_array_5, float_array_6 ) );
	print("");	

	'''

	PNG as float array interchange:
	
	 1.  Create float array.
	 2.  Convert float array to RGBA buffer.
	 3.  Write RGBA buffer to disk as .png.
	 4.  Read back .png from disk as RGBA buffer.
	 5.  Convert RGBA buffer to float array.
	 6.  Compare converted float array to original float array

	'''
	file_name = "rgba_buffer_4.png"
	width = 1024;
	height = 512;

	float_array_7 = generate_float_array( width, height );
	rgba_buffer_4 = float_array_to_rgba_buffer( float_array_7 );
	write_png( "rgba_buffer_4.png", rgba_buffer_4 );
	rgba_buffer_5 = read_png( "rgba_buffer_4.png" );
	float_array_8 = rgba_buffer_to_float_array( rgba_buffer_5 );

	print( "float_array_7 ~ float_array_8:");
	print( numpy.isclose( float_array_7, float_array_8 ) );
	print("");	

	print( "Have a nice day!  :)" );

if __name__ == "__main__":
	main();