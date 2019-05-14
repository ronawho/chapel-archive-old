module M1 {
  record A {
    var x = 1;

    proc foo() {
      writeln("In A.foo()");
    }
  }
}

module M2 {
  proc main() {
    use M1 only;

    var a = new M1.A(3); // One via the module prefix
    writeln(a.x); //essible because we have a record instance
    a.foo(); // Ditto
  }
}
