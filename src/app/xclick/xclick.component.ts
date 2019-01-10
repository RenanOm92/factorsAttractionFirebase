import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from "../data.service";

@Component({
  selector: 'app-xclick',
  templateUrl: './xclick.component.html',
  styleUrls: ['./xclick.component.css']
})
export class XclickComponent{

	myStyle = {};

	constructor(private router: Router, private dataService: DataService) { }
	
	myEvent(event) {		
		
		this.dataService.setUserPositionLeft(event.clientX);
	    this.dataService.setUserPositionTop(event.clientY);
		this.myStyle = {
			'left' : event.clientX+'px',
			'top' : event.clientY+'px'
			};

		this.router.navigateByUrl('/end');
	}

	btnClick() {
        this.router.navigateByUrl('/end');
	};

}
