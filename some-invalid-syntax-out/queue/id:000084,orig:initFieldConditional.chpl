class Point {
  var x, y : real;
  var r, theta : real;

  proc init(polar : bool, val : real) {
    if polar {
      //serts initialization for fields 'x' and 'y'
      this.r = val;
    } else {
      this.x = val;
      this.y = val;
      // coer inserts initialization for field 'r'
    }
    // comserts initialization for field 'theta'
  }
}

var A = new Point(true, 5.0);
var B = new Point(false, 1.0);
writeln(A);
writeln(B);
