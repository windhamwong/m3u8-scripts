import os, argparse, random, string

def main(args):
  filelist = os.listdir(args.path)
  prefix = filelist[0].split('-')[0]
  postfix = '-'.join(filelist[0].split('-')[2:])

  output = '%s/temp.mp4' % (args.path)
  try:
    os.remove(output)
  except:
    next

  with open(output, 'ab+') as f:
    for i in range(1, len(filelist)+1):
      if not os.path.exists('%s/%s-%s-%s' % (args.path, prefix, str(i), postfix)):
        print("Missing file %s-%s-%s" % (prefix, str(i), postfix))
        continue
      with open('%s/%s-%s-%s' % (args.path, prefix, str(i), postfix), 'rb') as f2:
        f.write(f2.read())

  os.system('ffmpeg -i %s -c copy %s/%s' % (output, args.path, args.name))
  print('[*] Done.')

  os.remove(output)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--path", dest="path", required=True)
  parser.add_argument("--filename", dest="name", required=True)

  args = parser.parse_args()


  main(args)
