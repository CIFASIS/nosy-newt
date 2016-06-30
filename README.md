# Nosy Newt <img src="https://raw.githubusercontent.com/CIFASIS/nosy-newt/master/logo.png" width="40">

Nosy Newt is a simple concolic execution tool for exploring the input space of a binary executable programs. I created this POC because i could not find any better tool for this. It is extensively using [Triton](http://triton.quarkslab.com/) for almost everything (hooking, solving constrains, etc).

## Use cases

Nosy Newt is designed to discover new inputs to trigger different paths in your binary using concolic execution. It requires to:

1. Select a program that reads a file.
2. Create a "inputs" directory with at least one file.
3. Launch nosy newt indicating the input file in the argument using "@@".
4. Wait for more inputs to be discover.

## Requirements

* [Triton](https://github.com/JonathanSalwan/Triton)
* Some dedicated RAM memory (at least 4 GB).
* Time.

## Installation

1. [Install Triton with PIN support](http://triton.quarkslab.com/documentation/doxygen/index.html#install_sec)
2. Install the Triton python module locally
3. Copy the "triton" script to your PATH (usually ~/.local/bin)
4. Install Nosy Newt:

```bash
    $ git clone https://github.com/CIFASIS/nosy-newt
    $ cd nosy-newt
    $ python setup.py install --local
```

## Example

    $ mkdir inputs
    $ python -c "print 'a'*24" > inputs/input.dat 
    $ ./newt.py -n 3 -i inputs "unzip -l @@"
    Using ['unzip', '-l', 'test.dat'] as arguments
    Exploring inputs/input.dat executing unzip
    Archive:  test.dat
    Hooking read of test.dat
    symbolized 0x71af20L with 0x61L
    ...
    symbolized 0x71af38L with 0xaL
      End-of-central-directory signature not found.  Either this file is not
      a zipfile, or it constitutes one disk of a multi-part archive.  In the
      latter case the central directory and zipfile comment will be found on
      the last disk(s) of this archive.
    unzip:  cannot find zipfile directory in one of test.dat or
            test.dat.zip, and cannot find test.dat.ZIP, period.
    Solving path conditions..
    Dumping inputs/-7819407262199667705.dat with 'aaaPaaaaaaaaaaaaaaaaaaaa\n'
    Solving path conditions..
    Dumping inputs/-43234624507741908.dat with 'aaP\xafaaaaaaaaaaaaaaaaaaaa\n'
    Solving path conditions..
    Dumping inputs/-8008955989580669208.dat with 'aP\xaf\xafaaaaaaaaaaaaaaaaaaaa\n'
    Solving path conditions..
    Dumping inputs/-1547994686380196427.dat with 'P\xaf\xaf\xafaaaaaaaaaaaaaaaaaaaa\n'
    Exploring inputs/-8008955989580669208.dat executing unzip
    ...


## TODO:

- Better exploration system (now just random)
- Shared library support
- Emulated syscalls (for detecting I/O)
  - [x] open
  - [x] read
  - [x] mmap (basic)
  - [ ] close
  - [ ] seek
- Website + Documentation
