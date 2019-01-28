import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

import { AngularFirestore } from '@angular/fire/firestore';

import { Observable } from 'rxjs';

export interface dataPositionOfX { email: string; device: string; screenSize: string; coord_original_left: string; coord_original_top: string; coord_user_left: string; coord_user_top: string;}

@Component({
  selector: 'app-end',
  templateUrl: './end.component.html',
  styleUrls: ['./end.component.css']
})
export class EndComponent implements OnInit {
	
	email: string;
  device: string;
  screenSize: string;
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
    this.originalLeft = this.dataService.getRandomPositionLeft().toString()+'px';
	  this.originalTop = this.dataService.getRandomPositionTop().toString()+'px';
	  this.userLeft = this.dataService.getUserPositionLeft().toString()+'px';
	  this.userTop = this.dataService.getUserPositionTop().toString()+'px';

	  var email = this.email;
    var device = this.device;
    var screenSize = this.screenSize;
    var coord_original_left = this.originalLeft;
  	var coord_original_top = this.originalTop;
  	var coord_user_left = this.userLeft;
  	var coord_user_top = this.userTop;

  	  const objectXPosition: dataPositionOfX = {email,device,screenSize,coord_original_left,coord_original_top,coord_user_left,coord_user_top};
      this.db.collection('1.1').add(objectXPosition);
  }

  btnClick() {
        this.router.navigateByUrl('/instructions');
	};

}