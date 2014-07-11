from server_info import *
#import nagios_summary
def process_info():
# Print the HTTP header info
    print "Content-Type: text/plain"
    print

# Now print the actual data
    try:
       for timer in range(1,500,25):
            t = Timer(timer, pretty_print_status)
	    t.start()
	    print "Ok I am done"
#        pretty_print_status()
#           list1 = pretty_print_status()[0]
#           list2 = pretty_print_status()[1]
#           list3 = pretty_print_status()[2]
#           list4 = pretty_print_status()[3]
#            output(test, "Sheet 1", pretty_print_status()[0], pretty_print_status()[1], pretty_print_status()[2], pretty_print_status()[3])
    except Exception, e:
            print "Internal Error -", e

