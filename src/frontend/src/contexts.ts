import { createContext } from 'react';

import {ProductShortType, SearchQuery} from "./types";

export const SubsectionModalContext =
  createContext<((subUrl?: string) => () => void) | undefined>(undefined);

export const SearchContext =
  createContext<((searchQuery: SearchQuery) => void) | null>(null);

export const ModalContext =
  createContext<[ProductShortType] | null>(null);
