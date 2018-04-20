# euca.me
DNS for your eucalyptus cloud.

Use euca.me with proof-of-concept or home installs of [eucalyptus cloud](https://eucalyptus.cloud/) with a single ufs host where dns cannot otherwise be configured.

Configuration
------

```
# euctl system.dns.dnsdomain
system.dns.dnsdomain = my-cloud-10-10-10-10.euca.me
```


Examples
------

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


FastStart using euca.me
------

To install via FastStart using euca.me dns:

```
bash <(curl -Ls https://go.euca.me)
```

FastStart is for non-production installs on a single host.
