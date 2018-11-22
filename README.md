<h1 align="center">python-splice</h1>
<p align="center">A Python interface to splice(2) syscall</p>


### About

```python3
# copy data from one file to another

from splice import splice

to_read = open("read.txt") # file to read from
to_write = open("write.txt", "w+") # file to write to

# pass file descriptors
splice(to_read.fileno(), to_write.fileno())
```

### Why

### Benchmark

### API Documentation

### Contribute

### License
