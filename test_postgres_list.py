import psycopg2
import sys


errors = [
  {'part': 'hba', 'desc': 'no pg_hba.conf entry'},
  {'part': 'timeout', 'desc': 'no network connection (reached timeout)'},
  {'part': 'refused', 'desc': 'connection refused'},
  {'part': 'database', 'desc': 'no database'},
]
output_ok = 'output_ok.txt'

outputs = [ 'output_{}.txt'.format(x['part']) for x in errors ]
outputs.append(output_ok)


def add_url(name, url):
  with open(name, 'a') as f:
    addr = url.split('@')[1]
    f.write("{}\n".format(addr))

def file_write(name, mode, value):
  with open(name, mode) as f:
    f.write(value)

def clear_outputs():
  for name in outputs:
    file_write(name, 'w', '')

def main():
  input_file = sys.argv[1]
  with open(input_file, 'r') as f:
    for url in f:
      url = url.strip()
      print(url)
      try:
        db = psycopg2.connect(url, connect_timeout=3)
        add_url(output_ok, url)
        print('ok')
      except Exception as e:
        type, value, traceback = sys.exc_info()
        err = str(value)
        found = False
        for error in errors:
          if error['part'] in err:
            add_url('output_{}.txt'.format(error['part']), url)
            print(error['desc'])
            found = True
            break
        if not found:
          add_url('output_else.txt', url)
          print(error)

if __name__ == '__main__':
  main()

