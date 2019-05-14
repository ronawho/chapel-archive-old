class C {
  var i,j,k: int;
}
var c : unmanaged C = nil;
delete c;      // Does nothing: c is nil.

c = new unmanaged C(); // Crct.
delete c;              // Det.

// The following statements reference an object after it has been deleted, so
// the behavior of each is "undefined":
// writeln(c.i); // May read from freed memory.
// c.i = 3;      // May overwrite freed memory.
// delete c;     // May confuse some allocators.
