import { Injectable } from '@angular/core';

@Injectable()
export class DataService {

  constructor() { }

  private randomPositionLeft;
	private randomPositionTop;

	private userPositionLeft;
	private userPositionTop;

  private email;

  	setRandomPositionLeft(data){
    	this.randomPositionLeft = data;
  	}

  	getRandomPositionLeft(){
    	return this.randomPositionLeft;
  	}

  	setRandomPositionTop(data){
    	this.randomPositionTop = data;
  	}

  	getRandomPositionTop(){
    	return this.randomPositionTop;
  	}

  	setUserPositionLeft(data){
    	this.userPositionLeft = data;
  	}

  	getUserPositionLeft(){
    	return this.userPositionLeft;
  	}

  	setUserPositionTop(data){
    	this.userPositionTop = data;
  	}

  	getUserPositionTop(){
    	return this.userPositionTop;
  	}

    setEmail(data){
      this.email = data;
    }

    getEmail(){
      return this.email;
    }
}
