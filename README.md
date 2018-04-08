# euca.me
DNS for your eucalyptus cloud:

```
# euctl system.dns.dnsdomain
system.dns.dnsdomain = my-cloud-10-10-10-10.euca.me
```

Examples:

```
# dig +short ec2.my-cloud-10-10-10-10.euca.me
10.10.10.10
```

```
# dig +short bucket.s3.my-cloud-10-10-10-10.euca.me
10.10.10.10
```

```
# dig +short euca-10-20-30-40.eucalyptus.my-cloud-10-10-10-10.euca.me
10.20.30.40
```
