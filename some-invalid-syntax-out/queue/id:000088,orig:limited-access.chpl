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

    var a = new M1.A(3); // Only accessible via the module prefix
    writeln(a.x); // Accessible because we have a record instance
    a.foo(); // Ditto
  }
}
