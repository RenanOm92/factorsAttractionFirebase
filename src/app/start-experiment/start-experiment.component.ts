import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from "../data.service";

@Component({
  selector: 'app-start-experiment',
  templateUrl: './start-experiment.component.html',
  styleUrls: ['./start-experiment.component.css']
})
export class StartExperimentComponent implements OnInit {

	leftPositionImage;
	topPositionImage;

	showFace = false;
	
	constructor(private router: Router, private dataService: DataService) {
	}

	
	// On the initialization, set a counter to change pages after X ms.
	ngOnInit() {
		
		this.conditionDecider(); // Check which condition should be shown

		this.getPositionX(); // Get the positon of the X

		setTimeout(() => {
	        this.router.navigate(['fillup']);
	    }, 1000);  //1s
   
	}

	conditionDecider(){
    var condition = this.dataService.getCondition();

    if (condition == "Face"){
      this.showFace = true;
    	}
  	}

  	getPositionX(){
  		// Sets the position of the X on a variable accesible globally
    	this.leftPositionImage = this.dataService.getRandomPositionLeft().toString()+"px";
    	this.topPositionImage = this.dataService.getRandomPositionTop().toString()+"px";
  	}
}
