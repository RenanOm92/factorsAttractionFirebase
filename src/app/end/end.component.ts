import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

import { AngularFirestore } from '@angular/fire/firestore';

import { Observable } from 'rxjs';

export interface dataPositionOfX { email: string; device: string; screenSize: string; condition: string; coord_original_left: string; coord_original_top: string; coord_user_left: string; coord_user_top: string;}

@Component({
  selector: 'app-end',
  templateUrl: './end.component.html',
  styleUrls: ['./end.component.css']
})
export class EndComponent implements OnInit {
	
	email: string;
  device: string;
  screenSize: string;
  condition: string;
  originalLeft: string;
	originalTop : string;
	userLeft: string;
	userTop: string;

  constructor(private router: Router, private dataService: DataService, private db: AngularFirestore) {
  }

  ngOnInit() {
	this.email = this.dataService.getEmail();
    this.device = this.dataService.getDevice();
    this.screenSize = this.dataService.getScreenSize();
    this.condition = this.dataService.getCondition();
    this.originalLeft = this.dataService.getRandomPositionLeft().toString()+'px';
	this.originalTop = this.dataService.getRandomPositionTop().toString()+'px';
	this.userLeft = this.dataService.getUserPositionLeft().toString()+'px';
	this.userTop = this.dataService.getUserPositionTop().toString()+'px';

	var email = this.email;
    var device = this.device;
    var screenSize = this.screenSize;
    var condition = this.condition;
    var coord_original_left = this.originalLeft;
  	var coord_original_top = this.originalTop;
  	var coord_user_left = this.userLeft;
  	var coord_user_top = this.userTop;

	const objectXPosition: dataPositionOfX = {email,device,screenSize,condition,coord_original_left,coord_original_top,coord_user_left,coord_user_top};
	this.db.collection('1.3').add(objectXPosition);
	this.generateNewCondition();
  }

  generateNewCondition(){
    var Totalconditions = 9;
    // 0 = calibration/default nothing with black fillout
    // 1,2,3 = face on the start and end background
    // 4 = spiral on the middle of the screen fill-out, size of spiral always half of the min between screen width and height, example 800x400, spiral will be 200x200.
    // 5 = spiral on the left top of the screen fill-out, size of spiral always half of the screen width, and height follows equal value to width. 800x400, spiral will be 400x400.
    // 6 = spiral on the right top of the screen fill-out, size of spiral always half of the screen width, and height follows equal value to width. 800x400, spiral will be 400x400.
    // 7 = click here button on the fill-out on the bottom left of the screen. 20% of screen size of distance to the edge. So if screen is 800x400, there will be 160px on the left and 100px on the bottom
    // 8 = click here button on the fill-out on the top right of the screen. 20% of screen size of distance to the edge. So if screen is 800x400, there will be 160px on the right and 100px on the top
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