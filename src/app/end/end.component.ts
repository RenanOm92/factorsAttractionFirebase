import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

import { AngularFirestore } from '@angular/fire/firestore';

import { Observable } from 'rxjs';

export interface dataPositionOfX { email: string; screenSize: string; originalLeft: string; originalTop: string; userLeft: string; userTop: string;}

@Component({
  selector: 'app-end',
  templateUrl: './end.component.html',
  styleUrls: ['./end.component.css']
})
export class EndComponent implements OnInit {
	
	email: string;
  screenSize: string;
  originalLeft: string;
	originalTop : string;
	userLeft: string;
	userTop: string;

  constructor(private router: Router, private dataService: DataService, private db: AngularFirestore) {
  }

  ngOnInit() {
	  this.email = this.dataService.getEmail();
    this.screenSize = this.dataService.getScreenSize();
    this.originalLeft = this.dataService.getRandomPositionLeft().toString()+'px';
	  this.originalTop = this.dataService.getRandomPositionTop().toString()+'px';
	  this.userLeft = this.dataService.getUserPositionLeft().toString()+'px';
	  this.userTop = this.dataService.getUserPositionTop().toString()+'px';

	  var email = this.email;
    var screenSize = this.screenSize;
    var originalLeft = this.originalLeft;
  	var originalTop = this.originalTop;
  	var userLeft = this.userLeft;
  	var userTop = this.userTop;

  	  const objectXPosition: dataPositionOfX = {email,screenSize,originalLeft,originalTop,userLeft,userTop};
      this.db.collection('1.2').add(objectXPosition);
  }

  btnClick() {
        this.router.navigateByUrl('/start');
	};

}