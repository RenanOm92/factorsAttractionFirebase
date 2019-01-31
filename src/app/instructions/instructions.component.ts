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
  	var Totalconditions = 2;
  	// 0 = calibration/default nothing with black fillout
  	// 1 = face on the start and end background
  	var conditionToBePlayed = this.getRandomInt(0,Totalconditions-1);

 	switch (conditionToBePlayed) {
 		case 0:
 			this.dataService.setCondition("Calibration");
 			break;
 		case 1:
 			this.dataService.setCondition("Face");
 			break;
 		default:
 			// code...
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
