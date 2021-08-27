import { TestBed } from '@angular/core/testing';

import { NimrodService } from './nimrod.service';

describe('NimrodService', () => {
  let service: NimrodService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NimrodService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
