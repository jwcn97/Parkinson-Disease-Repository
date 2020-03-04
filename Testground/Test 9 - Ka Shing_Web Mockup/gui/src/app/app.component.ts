import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  server = '';

  constructor(private http: HttpClient) {
  }

  ngOnInit(): void {
    // Test function 1
  }

  address(str: string): string {
    return this.server + str;
  }

  testFunctions() {
    if (this.server !== '') {
      // Check if correct server
      this.http.get(this.address('/get')).subscribe(x => {
        console.log(x);
      });
    } else {
      console.log('Invalid server name');
    }
  }
}

// # Functions
// @app.route('/function1')
// def function1():
// 	return 'Function1 working'

// @app.route('/function2')
// def function2():
// 	return 'Function2 is also working!'

// # Attempt GET
// @app.route('/get', methods = ['GET'])
// def get():
// 	return 'Something'

// # Attempt POST
// @app.route('/post', methods = ['POST'])
// def request(i):
// 	global p_var

// 	p_var += i

// @app.route('/postgetwithget', methods = ['GET'])
// def request_get():
// 	return p_var

// @app.route('/postgetwithoutget')
// def request_get_without_get():
// 	return p_var

// # Attempt GET and POST
// @app.route('/', methods = ['GET', 'POST'])
// def get_and_post(i):
// 	global gp_var

// 	gp_var += i

// 	return gp_var
