import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

import { AngularFirestore } from '@angular/fire/firestore';

import { Observable } from 'rxjs';

export interface dataPositionOfX { email: string; originalLeft: string; originalTop: string; userLeft: string; userTop: string;}

@Component({
  selector: 'app-end',
  templateUrl: './end.component.html',
  styleUrls: ['./end.component.css']
})
export class EndComponent implements OnInit {
	
	email: string;
  originalLeft: string;
	originalTop : string;
	userLeft: string;
	userTop: string;

  constructor(private router: Router, private dataService: DataService, private db: AngularFirestore) {
  }

  ngOnInit() {
	  this.email = this.dataService.getEmail();
    this.originalLeft = this.dataService.getRandomPositionLeft().toString()+'px';
	  this.originalTop = this.dataService.getRandomPositionTop().toString()+'px';
	  this.userLeft = this.dataService.getUserPositionLeft().toString()+'px';
	  this.userTop = this.dataService.getUserPositionTop().toString()+'px';

	  var email = this.email;
    var originalLeft = this.originalLeft;
  	var originalTop = this.originalTop;
  	var userLeft = this.userLeft;
  	var userTop = this.userTop;

  	  const objectXPosition: dataPositionOfX = {email,originalLeft,originalTop,userLeft,userTop};
  	  //this.db.collection('items').doc('email').set(objectXPosition);
      this.db.collection('items').add(objectXPosition);
  }

  btnClick() {
        this.router.navigateByUrl('/instructions');
	};

}