#!/usr/bin/python -u
import re
import sys


class PowerDnsQuery(object):
    ttl = 30
    sip = '127.0.0.1'

    def __init__(self, query):
        (_type, qname, qclass, qtype, _id, ip) = query
        self.has_result = False
        qname_lower = qname.lower()

        self.results = []

        if (qtype == 'SOA' or qtype == 'ANY') and qname_lower == 'euca.me':
            self.results.append(
                'DATA\t%s\t%s\tSOA\t%d\t-1\tns1.euca.me\tadmin.euca.me\t'
                '2018031400\t1800\t900\t604800\t900'
                % (qname, qclass, PowerDnsQuery.ttl))
            self.has_result = True

        if (qtype == 'NS' or qtype == 'ANY') and qname_lower == 'euca.me':
            self.results.append('DATA\t%s\t%s\tNS\t%d\t-1\tns1.euca.me'
                                % (qname, qclass, PowerDnsQuery.ttl))
            self.has_result = True

        if (qtype == 'MX' or qtype == 'ANY') and qname_lower == 'euca.me':
            self.results.append(
                'DATA\t%s\t%s\tMX\t%d\t-1\t5\tgmr-smtp-in.l.google.com'
                % (qname, qclass, PowerDnsQuery.ttl))
            self.results.append(
                'DATA\t%s\t%s\tMX\t%d\t-1\t10\talt1.gmr-smtp-in.l.google.com'
                % (qname, qclass, PowerDnsQuery.ttl))
            self.results.append(
                'DATA\t%s\t%s\tMX\t%d\t-1\t20\talt2.gmr-smtp-in.l.google.com'
                % (qname, qclass, PowerDnsQuery.ttl))
            self.has_result = True

        if (qtype == 'CNAME' or qtype == 'ANY') and \
                qname_lower == 'www.euca.me':
            self.results.append(
                'DATA\t%s\t%s\tCNAME\t%d\t-1\t%s'
                % (qname, qclass, PowerDnsQuery.ttl,
                   'dj3ltynlr0evw.cloudfront.net'))
            self.has_result = True

        if (qtype == 'CNAME' or qtype == 'ANY') and \
                qname_lower == 'go.euca.me':
            self.results.append(
                'DATA\t%s\t%s\tCNAME\t%d\t-1\t%s'
                % (qname, qclass, PowerDnsQuery.ttl,
                   'd3rahf8dg1z1ts.cloudfront.net'))
            self.has_result = True

        if (qtype == 'A' or qtype == 'ANY') and \
                qname_lower == 'euca.me':
            # http server
            self.results.append(
                'DATA\t%s\t%s\tA\t%d\t-1\t%s'
                % (qname, qclass, PowerDnsQuery.ttl, PowerDnsQuery.sip))
            self.has_result = True

        elif (qtype == 'A' or qtype == 'ANY') and \
                re.match('^ns[1-9]\.euca\.me$', qname_lower):
            # name servers
            self.results.append(
                'DATA\t%s\t%s\tA\t%d\t-1\t%s'
                % (qname, qclass, PowerDnsQuery.ttl, PowerDnsQuery.sip))
            self.has_result = True

        elif (qtype == 'A' or qtype == 'ANY') and re.match(
                '^ec2-(\d{1,3})-(\d{1,3})-(\d{1,3})-(\d{1,3})\.compute\.'
                '[a-z0-9-]{0,32}?\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}\.euca\.me$',
                qname_lower):
            # instances, ...
            match = re.match(
                '^ec2-(\d{1,3})-(\d{1,3})-(\d{1,3})-(\d{1,3})\.compute\.'
                '[a-z0-9-]{0,32}?\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}\.euca\.me$',
                qname_lower)
            self.results.append(
                'DATA\t%s\t%s\tA\t%d\t-1\t%s'
                % (qname, qclass, PowerDnsQuery.ttl,
                   '%s.%s.%s.%s' % match.groups()))
            self.has_result = True

        elif (qtype == 'A' or qtype == 'ANY') and re.match(
                '^euca-(\d{1,3})-(\d{1,3})-(\d{1,3})-(\d{1,3})\.eucalyptus\.'
                '[a-z0-9-]{0,32}?\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}\.euca\.me$',
                qname_lower):
            # instances, ...
            match = re.match(
                '^euca-(\d{1,3})-(\d{1,3})-(\d{1,3})-(\d{1,3})\.eucalyptus\.'
                '[a-z0-9-]{0,32}?\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}\.euca\.me$',
                qname_lower)
            self.results.append(
                'DATA\t%s\t%s\tA\t%d\t-1\t%s'
                % (qname, qclass, PowerDnsQuery.ttl,
                   '%s.%s.%s.%s' % match.groups()))
            self.has_result = True

        elif (qtype == 'A' or qtype == 'ANY') and re.match(
                '^(?:[a-z0-9-.]{3,63}\.)?[a-z0-9]{1,32}\.[a-z0-9-]{0,32}?'
                '(\d{1,3})-(\d{1,3})-(\d{1,3})-(\d{1,3})\.euca\.me$',
                qname_lower):
            # services ec2, s3, mybucket.s3, ...
            match = re.match(
                '^(?:[a-z0-9-.]{3,63}\.)?[a-z0-9]{1,32}\.[a-z0-9-]{0,32}?'
                '(\d{1,3})-(\d{1,3})-(\d{1,3})-(\d{1,3})\.euca\.me$',
                qname_lower)
            self.results.append(
                'DATA\t%s\t%s\tA\t%d\t-1\t%s'
                % (qname, qclass, PowerDnsQuery.ttl,
                   '%s.%s.%s.%s' % match.groups()))
            self.has_result = True

    def get_result(self):
        if self.has_result:
            return '\n'.join(self.results)
        else:
            return ''


class PowerDnsHandler(object):

    def __init__(self, dnsin, dnsout):
        self.dnsin = dnsin
        self.dnsout = dnsout
        self.handle_requests()

    def handle_requests(self):
        first_request = True
        while 1:
            rawline = self.dnsin.readline()
            if rawline == '':
                return
            line = rawline.rstrip()

            if first_request:
                if line == 'HELO\t1':
                    self.write('OK\tStarting handler')
                else:
                    self.write('FAIL')
                    rawline = self.dnsin.readline()
                    sys.exit(1)
                first_request = False
            else:
                query = line.split('\t')
                if len(query) != 6:
                    self.write('LOG\tError parsing query')
                    self.write('FAIL')
                else:
                    pd_query = PowerDnsQuery(query)
                    if pd_query.has_result:
                        pdns_result = pd_query.get_result()
                        self.write(pdns_result)
                    self.write('END')

    def write(self, message):
        self.dnsout.write(message + '\n')
        self.dnsout.flush()


if __name__ == '__main__':
    PowerDnsHandler(sys.stdin, sys.stdout)
