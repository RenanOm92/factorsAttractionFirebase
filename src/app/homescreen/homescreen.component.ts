import { Component, NgModule  } from '@angular/core';
import { Router } from '@angular/router';
import { NgForm }   from '@angular/forms';
import { DataService } from "../data.service";


@Component({
  selector: 'app-homescreen',
  templateUrl: './homescreen.component.html',
  styleUrls: ['./homescreen.component.css']
})
export class HomescreenComponent {

	constructor(private router: Router, private dataService: DataService){}

	email: string;
	isValidFormSubmitted = null;
	emailPattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$";	
	
	onSubmit(form: NgForm) {
		this.isValidFormSubmitted = false;
     	if (form.invalid) {
        	return;
     	}
     	this.isValidFormSubmitted = true;
  		this.dataService.setEmail(this.email);
        this.router.navigateByUrl('/instructions');
	};
}

