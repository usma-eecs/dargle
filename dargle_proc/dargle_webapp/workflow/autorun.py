import request, dargle_orm, sys

innie = sys.argv[1]
outie = sys.argv[2]
# thread_num = int(sys.argv[3])
domain = sys.argv[3]
header = sys.argv[4]

request.line_count(innie)

csv = request.process_links(innie,outie,header)
# csv = outie
dargle_orm.dbUpdate(csv,domain)
