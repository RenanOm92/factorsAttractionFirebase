import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StartExperimentComponent } from './start-experiment.component';

describe('StartExperimentComponent', () => {
  let component: StartExperimentComponent;
  let fixture: ComponentFixture<StartExperimentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StartExperimentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StartExperimentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
