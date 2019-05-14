var D : domain(string);
var A : [D] int;
A["a"] = 1;
A["b"] = 2;
var x = A["a"];
// writeln(A["c"]); // halts if "c" is not in A's domain
