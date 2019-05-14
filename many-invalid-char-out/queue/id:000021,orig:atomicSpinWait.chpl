var x: atomic int;
cobegin {
  while x.read() != 1 do ;  // spinzes processor
  x.write(1);
}
