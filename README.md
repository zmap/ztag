# ZTag

[![Build Status](https://travis-ci.org/zmap/ztag.svg?branch=master)](https://travis-ci.org/zmap/ztag)

ZTag is a utility that works in conjunction with ZMap and ZGrab and allows 
annotating raw scan data with additional metadata (e.g., device models and 
vulnerabilities) and transforming records. ZTag is used extensively within
Censys (https://www.censys.io) to produce the data present in the search
engine. However, it can also be run independently with ZMap and ZGrab.

## Installation

ZTag follows the standard Python setup.py flow.

```
python setup.py build
python setup.py install
```

## Basic Usage

ZTag consumes the JSON output from [ZGrab](https://github.com/zmap/zgrab)
scanner and then produces its own JSON output. Most simply, these JSON documents
can be piped into ztag. For example, when processing an HTTP ZGrab Scan:

	cat http.json | ztag -p 80 -P http -S get

There is a long list of protocol/subprotocol combinations that exist but are not
particularly well documented.
