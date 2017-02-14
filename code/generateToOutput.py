import os.path
solsDir = 'phase2-sols/'
cyclesDir = 'phase1-cycles/'
toOutputFile = 'toOutput.txt'

def main():
	with open(toOutputFile, 'w') as file:
		for instance in range(1,493):
			cyclesFile = cyclesDir + str(instance) + '.in'
			solsFile = solsDir + str(instance) + '.out'
			if os.path.isfile(cyclesFile):
				if not os.path.isfile(solsFile):
					file.write('{0}\n'.format(instance))

if __name__ == '__main__':
	main()