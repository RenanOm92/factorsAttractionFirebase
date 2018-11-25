import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-fill-up',
  templateUrl: './fill-up.component.html',
  styleUrls: ['./fill-up.component.css']
})
export class FillUpComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit() {
		
		setTimeout(() => {
	        this.router.navigate(['xclick']);
	    }, 500);  //0.5s
   
	}

}
