// This test case represents a bug originally reported in issue #7783

class A{
  forwarding var driver: B;
}

class B{
  type MyType = 3*string; //This makes the compiler not find the overridden methods.

  var bfield:MyType; 

  proc foo1(){
     return this;
  }

  proc foo2(args2:string){
      return this;
  }

  proc foo3(args3, args4:string){
      return this;
  }
  proc foo4(arg){
     return this;
  }

}

class C:B{

  var cfield:int;
}


var c1 = new A(new C());
writeln(c1.foo1());

var c2 = new A(new C());
writeln(c2.foo2("Test"));

var c3 = new A(new C());
writeln(c3.foo3("Test", "Test"));

var c4 = new A(new C());
writeln(c4.foo4("Test"));
