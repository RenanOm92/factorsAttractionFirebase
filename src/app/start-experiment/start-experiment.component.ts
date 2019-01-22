import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HostListener } from "@angular/core";
import { DataService } from "../data.service";

@Component({
  selector: 'app-start-experiment',
  templateUrl: './start-experiment.component.html',
  styleUrls: ['./start-experiment.component.css']
})
export class StartExperimentComponent implements OnInit {

	// Initialization of variables
	screenHeight = 0;
	screenWidth = 0;
	
	leftPositionImage;
	topPositionImage;
	
	constructor(private router: Router, private dataService: DataService) {
		this.onResize(); // Calls the method to get screenSize

		var randomNumber1;
		var randomNumber2;

		// Generates the position of the X, always careful to not be too close to the edges or the center.
		// The randomNumber will always be between 0 and 1 and it will be multiplied by the screen size
		// to generate the coordinates
		do {
			randomNumber1 = Math.random();
			if ((randomNumber1 > 0.05 && randomNumber1 < 0.45) || (randomNumber1 > 0.55 && randomNumber1 < 0.95)){
				this.dataService.setRandomPositionLeft(Math.floor(randomNumber1*this.screenWidth));
			}
		}while (this.dataService.getRandomPositionLeft == undefined);

		do {
			randomNumber2 = Math.random();
			if ((randomNumber2 > 0.05 && randomNumber2 < 0.45) || (randomNumber2 > 0.55 && randomNumber2 < 0.95)){
				this.dataService.setRandomPositionTop(Math.floor(randomNumber2*this.screenHeight));
			}
		}while (this.dataService.getRandomPositionTop == undefined);
		
		
		// Sets the position of the X on a variable accesible globally
		this.leftPositionImage = this.dataService.getRandomPositionLeft().toString()+"px";
		this.topPositionImage = this.dataService.getRandomPositionTop().toString()+"px";
	}

	
	// On the initialization, set a counter to change pages after X ms.
	ngOnInit() {
		setTimeout(() => {
	        this.router.navigate(['fillup']);
	    }, 1000);  //1s
   
	}
	
	// Gets the size of the screen, also listen in case of changing the screen size.
	@HostListener('window:resize', ['$event'])
    onResize(event?) {
      this.screenHeight = window.innerHeight;
      this.screenWidth = window.innerWidth;
      this.dataService.setScreenSize(this.screenWidth.toString()+"x"+this.screenHeight.toString());
	}
}
