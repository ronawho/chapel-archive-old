proc fillTuple(param p, x) {
  var result: p*x.type;
  for param i in 1..p do
    result(i) = x;
  return result;
}
var x = fillTuple(3, 3.14);
writeln(x);
writeln(x.type:string);
