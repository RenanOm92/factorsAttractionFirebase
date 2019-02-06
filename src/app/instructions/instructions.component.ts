import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from "../data.service";

@Component({
  selector: 'app-instructions',
  templateUrl: './instructions.component.html',
  styleUrls: ['./instructions.component.css']
})
export class InstructionsComponent implements OnInit{

  constructor(private router: Router, private dataService: DataService) { }

  ngOnInit() {
  	this.generateCondition();	
  };

  generateCondition(){
  	var Totalconditions = 9;
  	// 0 = calibration/default nothing with black fillout
  	// 1,2,3 = face on the start and end background
  	// 4 = spiral on the middle of the screen fill-out, size of spiral always half of the min between screen width and height, example 800x400, spiral will be 200x200.
    // 5 = spiral on the left top of the screen fill-out, size of spiral always half of the screen width, and height follows equal value to width. 800x400, spiral will be 400x400.
    // 6 = spiral on the right top of the screen fill-out, size of spiral always half of the screen width, and height follows equal value to width. 800x400, spiral will be 400x400.
    // 7 = click here button on the fill-out on the bottom left of the screen. 20% of screen size of distance to the edge. So if screen is 800x400, there will be 160px on the left and 100px on the bottom
    // 8 = click here button on the fill-out on the top right of the screen. 20% of screen size of distance to the edge. So if screen is 800x400, there will be 160px on the right and 100px on the top. 
  	// Buttom Click here will always have 87x32 pixels.
    var conditionToBePlayed = this.getRandomInt(0,Totalconditions-1);

 	switch (conditionToBePlayed) {
 		case 0:
 			this.dataService.setCondition("Calibration");
 			break;
 		case 1:
 			this.dataService.setCondition("Face");
 			break;
    case 2:
      this.dataService.setCondition("Face");
      break;
    case 3:
      this.dataService.setCondition("Face");
      break;
 		case 4:
 			this.dataService.setCondition("SpiralCenter")
 			break;
    case 5:
      this.dataService.setCondition("SpiralLeft")
      break;
    case 6:
      this.dataService.setCondition("SpiralRight")
      break;
    case 7:
      this.dataService.setCondition("ClickHereBottomLeft")
      break;
    case 8:
      this.dataService.setCondition("ClickHereTopRight")
      break;
 	  }
  }

  getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };

  btnClick() {  			
  		this.router.navigateByUrl('/start');
	};

}
