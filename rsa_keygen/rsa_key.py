import random, sys, os, rabinMiller, cryptomath, sha

def main():
	makeKeyFiles('RSA', 1024)
	
def generateKey(keySize):
	print('Generating p prime...')
	p = rabinMiller.generateLargePrime(keySize)
	print('Generating q prime...')
	q = rabinMiller.generateLargePrime(keySize)
	n = p * q
	# Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
	print('Generating e that is relatively prime to (p-1)*(q-1)...')
	while True:
		e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
		if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
			break
	print('Calculating d that is mod inverse of e...')
	d = cryptomath.findModInverse(e, (p - 1) * (q - 1))
	publicKey = (n, e)
	privateKey = (n, d)
	print('Public key:', publicKey)
	print('Private key:', privateKey)
	return (publicKey, privateKey)

def makeKeyFiles(name, keySize):
	if os.path.exists('%s_public_key.txt' % (name)) or os.path.exists('%s_private_key.txt' % (name)):
		sys.exit('WARNING: The file %s_public_key.txt or %s_private_key.txt already exists! Use a different name or delete these files and re-run this program.' % (name, name))
	publicKey, privateKey = generateKey(keySize)
	print()
	print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1])))) 
	print('Writing public key to file %s_public_key.txt...' % (name))   
	fo = open('%s_public_key.txt' % (name), 'w')
	fo.write('%s, %s' % (keySize, sha.digst(str(publicKey[0])+str(publicKey[1]))))
	fo.close()
	print()
	print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
	print('Writing private key to file %s_private_key.txt...' % (name))
	fo = open('%s_private_key.txt' % (name), 'w')
	fo.write('%s, %s' % (keySize, sha.digst(str(privateKey[0])+str(privateKey[1]))))
	fo.close()

if __name__ == '__main__':
   main()
