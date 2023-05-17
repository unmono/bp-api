import { createContext } from 'react';

export const SubsectionModalContext =
  createContext<((subUrl?: string) => () => void) | undefined>(undefined);
