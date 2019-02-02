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
      this.db.collection('1.2').add(objectXPosition);
      this.generateNewCondition();
  }

  generateNewCondition(){
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