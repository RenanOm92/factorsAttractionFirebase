import { Component } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-homescreen',
  templateUrl: './homescreen.component.html',
  styleUrls: ['./homescreen.component.css']
})
export class HomescreenComponent {

	constructor(private router: Router) { }

	btnClick() {
        this.router.navigateByUrl('/start');
	};
	
}

