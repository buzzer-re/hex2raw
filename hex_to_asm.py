import sys, os
import binascii
import argparse
import yaml


PREFIX_FILE = "prefix_address_size.yml"


def load_boards():
	boards_yaml = ""
	with open(PREFIX_FILE, "r") as address_yml:
		try:
			boards_yaml = yaml.safe_load(address_yml).get('boards')
		except Exception as e:
			print(e)
			boards_yaml = None
	
	return boards_yaml



if __name__ == '__main__':

	if os.path.exists(PREFIX_FILE) is False:
		print("Missing {}!".format(PREFIX_FILE))
		sys.exit(1)
	

	boards = load_boards()
	args = argparse.ArgumentParser(description="Convert .hex files into a raw hex dump")
	args.add_argument("--board", help="Board type, ex: atmega328p", type=str)
	args.add_argument("--output", help="Raw dump output path")
	args.add_argument("hexfile", help="Hex file")

	args = args.parse_args()
	
	

	
	if boards is None:
		print("Invalid {} file!".format(PREFIX_FILE))
		sys.exit(1)

	if args.board not in boards:
		print("No supported board {}".format(args.board))
		sys.exit(1)
	

	print("Parsing {}".format(args.hexfile))
		
	address_size = boards.get(args.board)
	raw_code = b''
	if args.output == None:
		args.output = "{}.dump".format(args.hexfile)

	with open(args.hexfile, "rb") as hex_file:
		for line in hex_file.readlines():
			line = line.rstrip()
			# Only data section, removes checksum
			data = line[address_size:-2]
			raw_code += binascii.unhexlify(data)


		with open(args.output, "wb") as raw:
			raw.write(raw_code)
			print("Written as {}".format(args.output))

