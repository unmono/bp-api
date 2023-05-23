import React, {ErrorInfo} from 'react';
import ErrorLayout from "./ErrorLayout";

type ErrorBoundaryProps = {
  children: React.ReactNode
}

type ErrorBoundaryState = {
  hasError: boolean,
  error: any
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {hasError: true, error: null};
  }

  static getDerivedStateFromError(error: any) {
    return {hasError: true, error: error};
  }

  render() {
    if (this.state.hasError) {
      const {code, message} = this.state.error;
      return <ErrorLayout code={code} message={message} />;
    }
    return this.props.children;
  }
}