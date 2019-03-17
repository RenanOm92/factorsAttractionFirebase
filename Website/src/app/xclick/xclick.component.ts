import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from "../data.service";

@Component({
  selector: 'app-xclick',
  templateUrl: './xclick.component.html',
  styleUrls: ['./xclick.component.css']
})
export class XclickComponent implements OnInit {

	myStyle = {};

	showFace = false;

	constructor(private router: Router, private dataService: DataService) { }

	ngOnInit() {
		this.conditionDecider(); // Check which condition should be shown
	}

	conditionDecider(){
		var condition = this.dataService.getCondition();

		if (condition == "Face"){
			this.showFace = true;
		}
	}
	
	myEvent(event) {		
		
		this.dataService.setUserPositionLeft(event.clientX);
	    this.dataService.setUserPositionTop(event.clientY);
		this.myStyle = {
			'left' : event.clientX+'px',
			'top' : event.clientY+'px'
			};

		this.router.navigateByUrl('/end');
	}

}
