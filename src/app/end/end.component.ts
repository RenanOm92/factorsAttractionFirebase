import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

import { AngularFirestore } from '@angular/fire/firestore';
import { Observable } from 'rxjs';


@Component({
  selector: 'app-end',
  templateUrl: './end.component.html',
  styleUrls: ['./end.component.css']
})
export class EndComponent implements OnInit {
	
	originalLeft;
	originalTop;
	userLeft;
	userTop;

	items: Observable<any[]>;

  constructor(private router: Router, private dataService: DataService,private db: AngularFirestore) {

  	this.items = db.collection('items').valueChanges();
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

}
