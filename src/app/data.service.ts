import { Injectable } from '@angular/core';

@Injectable()
export class DataService {

  constructor() { }

  private randomPositionLeft; // Coordinate generated on the X axes, based on the width of the screen on the start of the experiment
	private randomPositionTop; // Coordinate generated on the Y axes, based on the height of the screen

	private userPositionLeft; // Coordinate from the feedback of the user on the X axes
	private userPositionTop; // Coordinate from the feedback of the user on the Y axes

  private email;

  private screenSize; // Width x Height
  private device; // Touchscreen or mouse

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

  setScreenSize(data){
    this.screenSize = data;
  }

  getScreenSize(){
    return this.screenSize;
  }

  setDevice(data){
    this.device = data;
  }

  getDevice(){
    return this.device;
  }
}
