class C { }
// assume that C is a class
var a = new owned C();
var b:owned C; // initialized to store `nil`
b = a; // trownership from a to b
writeln(a); // a is left storing `nil`
