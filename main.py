import argparse
from app import app as Application

app = Application()

def add(host: str, service_type: str, feedback: int):
    app.add(host, service_type, feedback)


def remove(num_host : int):
    app.remove(num_host)


def check(num_host : int):
    host, result= app.check(num_host)
    print(host, "is worked!" if result else "isn't worked!")

def listofhosts():
    for i, item in enumerate(app.get_list()):
        print("["+ str(i) + "]", item.type_host, "\t:", item.source)


parser = argparse.ArgumentParser(
    prog='service-checker',
)
parser.add_argument("--verbose", help="Show output", action='store_true')
parser.add_argument("--errors", help="Show disabled services", action='store_true')
parser.add_argument("--add", type=str, help='Input your host')
parser.add_argument("--type", type=str,
                    help='Usage with --add, input type of your service')
parser.add_argument("--feedback", type=int,
                    help='Usage with --add, input answer of your service')
parser.add_argument("--remove", type=int,
                    help="Input number of service for removing")
parser.add_argument("--check", type=int,
                    help="Input number of service for checking")
parser.add_argument("--list", help="Show list of your services", action='store_true')

args = parser.parse_args()

debug = False
errors = False
if args.add != None and args.type != None and args.feedback != None and args.remove != True and args.check == None and args.list != True and args.errors != True and args.verbose != True:
    add(args.add, args.type, args.feedback)
elif args.remove != None  and args.add == None and args.check == None and args.list != True and args.type == None and args.feedback == None and args.errors != True and args.verbose != True:
    remove(args.remove)
elif args.check != None  and args.remove == None and args.add == None and args.list != True and args.type == None and args.feedback == None and args.errors != True and args.verbose != True:
    check(args.check)
elif args.list == True and args.remove == None and args.check == None and args.add == None and args.type == None and args.feedback == None and args.errors != True and args.verbose != True:
    listofhosts()
elif args.add == None and args.remove == None and args.check == None and args.list != True and args.type == None and args.feedback == None:
    if args.verbose:
        debug = True
    if args.errors:
        errors = True
    app.set(DEBUG=debug, ERRORS=errors)
    app.run()
else:
    parser.error('ты долбаеб!')
