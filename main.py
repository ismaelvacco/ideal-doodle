import broker

if __name__ == "__main__":
    for b in broker.getBrokers():
        print "%s = %s" % (b.CODE, b.getPrice())
