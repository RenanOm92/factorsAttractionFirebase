import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { XclickComponent } from './xclick.component';

describe('XclickComponent', () => {
  let component: XclickComponent;
  let fixture: ComponentFixture<XclickComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ XclickComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(XclickComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
