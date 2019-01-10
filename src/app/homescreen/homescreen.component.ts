import { Component, NgModule  } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule }   from '@angular/forms';
import { DataService } from "../data.service";


@Component({
  selector: 'app-homescreen',
  templateUrl: './homescreen.component.html',
  styleUrls: ['./homescreen.component.css']
})
export class HomescreenComponent {

	constructor(private router: Router, private dataService: DataService) { }

	email: string;

	btnClick() {
		this.dataService.setEmail('this.email');
        this.router.navigateByUrl('/instructions');
	};

	
	onSubmit() {
  		this.dataService.setEmail(this.email);
        this.router.navigateByUrl('/instructions');
	};
}

