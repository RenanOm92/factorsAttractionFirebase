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
  	var Totalconditions = 4;
  	// 0 = calibration/default nothing with black fillout
  	// 1 = face on the start and end background
  	// 2 = spiral on the middle of the screen fill-out
    // 3 = click here button on the fill-out
  	var conditionToBePlayed = this.getRandomInt(0,Totalconditions-1);

 	switch (conditionToBePlayed) {
 		case 0:
 			this.dataService.setCondition("Calibration");
 			break;
 		case 1:
 			this.dataService.setCondition("Face");
 			break;
 		case 2:
 			this.dataService.setCondition("Spiral")
 			break;
    case 3:
      this.dataService.setCondition("ClickHere")
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
