import os, argparse, random, string

def main(args):
  filelist = os.listdir(args.path)
  prefix = filelist[0].split('-')[0]
  postfix = '-'.join(filelist[0].split('-')[2:])

  output = '%s/%s' % (args.path, args.name)
  with open(output, 'ab+') as f:
    for i in range(1, len(filelist)+1):
      with open('%s/%s-%s-%s' % (args.path, prefix, str(i), postfix), 'rb') as f2:
        f.write(f2.read())
  print('[*] Done.')


  print(args)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--path", dest="path", required=True)
  parser.add_argument("--filename", dest="name", required=True)

  args = parser.parse_args()


  main(args)
