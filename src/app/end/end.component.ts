import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

import { AngularFirestore } from '@angular/fire/firestore';

import { Observable } from 'rxjs';

export interface dataX { originalLeft: string; originalTop: string; userLeft: string; userTop: string;}

@Component({
  selector: 'app-end',
  templateUrl: './end.component.html',
  styleUrls: ['./end.component.css']
})
export class EndComponent implements OnInit {
	
	originalLeft: string;
	originalTop : string;
	userLeft: string;
	userTop: string;

  constructor(private router: Router, private dataService: DataService, private db: AngularFirestore) {
  	//var originalLeft = this.originalLeft;
  	//var originalTop = this.originalTop;
  	//var userLeft = this.userLeft;
  	//var userTop = this.userTop;
  	
  	//const dataXX: dataX = {originalLeft,originalTop,userLeft,userTop};
  	//this.db.collection('items').doc('Testexx').set(dataXX);
  }

  ngOnInit() {
	  this.originalLeft = this.dataService.getRandomPositionLeft().toString()+'px';
	  this.originalTop = this.dataService.getRandomPositionTop().toString()+'px';
	  this.userLeft = this.dataService.getUserPositionLeft().toString()+'px';
	  this.userTop = this.dataService.getUserPositionTop().toString()+'px';
  }

  btnClick() {
        this.router.navigateByUrl('/homescreen');
	};

  addX(private originalLeft: string, private originalTop: string, private userLeft: string, private userTop: string){
  	const dataX: dataX = {originalLeft, originalTop, userLeft, userTop};
  	this.db.collection('items').doc('Testex').set(dataX);
  };

}