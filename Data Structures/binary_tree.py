from typing import Any, List, Optional


class Node:
    def __init__(self, item: Any):
        """
        이진 트리를 구성하는 노드를 초기화한다.

        Args:
            item (Any): 노드에 저장할 데이터
        """
        self.data = item
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

    def size(self) -> int:
        """
        현재 노드를 루트로 하는 (서브)트리의 노드 개수를 반환한다.

        Returns:
            int: (서브)트리의 전체 노드 수
        """
        l = self.left.size() if self.left else 0
        r = self.right.size() if self.right else 0
        return l + r + 1

    def depth(self) -> int:
        """
        현재 노드를 루트로 하는 (서브)트리의 깊이(높이)를 반환한다.

        정의:
            - 빈 트리의 깊이는 0
            - 노드가 하나만 있는 트리의 깊이는 1
            - 그 외에는 1 + max(왼쪽 깊이, 오른쪽 깊이)

        Returns:
            int: (서브)트리의 깊이
        """
        left_depth = self.left.depth() if self.left else 0
        right_depth = self.right.depth() if self.right else 0
        return 1 + max(left_depth, right_depth)

    def inorder(self) -> List[Any]:
        """
        중위 순회(In-order traversal) 결과를 리스트로 반환한다.

        방문 순서:
            left -> self -> right

        Returns:
            list: 중위 순회 결과(노드 데이터의 리스트)
        """
        traversal: List[Any] = []

        if self.left:
            traversal += self.left.inorder()

        traversal.append(self.data)

        if self.right:
            traversal += self.right.inorder()

        return traversal

    def preorder(self) -> List[Any]:
        """
        전위 순회(Pre-order traversal) 결과를 리스트로 반환한다.

        방문 순서:
            self -> left -> right

        Returns:
            list: 전위 순회 결과(노드 데이터의 리스트)
        """
        traversal: List[Any] = [self.data]

        if self.left:
            traversal += self.left.preorder()

        if self.right:
            traversal += self.right.preorder()

        return traversal

    def postorder(self) -> List[Any]:
        """
        후위 순회(Post-order traversal) 결과를 리스트로 반환한다.

        방문 순서:
            left -> right -> self

        Returns:
            list: 후위 순회 결과(노드 데이터의 리스트)
        """
        traversal: List[Any] = []

        if self.left:
            traversal += self.left.postorder()

        if self.right:
            traversal += self.right.postorder()

        traversal.append(self.data)

        return traversal


class BinaryTree:
    def __init__(self, r: Optional[Node]):
        """
        이진 트리를 초기화한다.

        Args:
            r (Node or None): 트리의 루트 노드. 빈 트리는 None을 사용한다.
        """
        self.root: Optional[Node] = r

    def size(self) -> int:
        """
        트리의 전체 노드 개수를 반환한다.

        Returns:
            int: 트리의 노드 수
        """
        if self.root:
            return self.root.size()
        else:
            return 0

    def depth(self) -> int:
        """
        트리의 깊이(높이)를 반환한다.

        Returns:
            int: 트리의 깊이
        """
        if self.root:
            return self.root.depth()
        else:
            return 0

    def inorder(self) -> List[Any]:
        """
        트리의 중위 순회 결과를 리스트로 반환한다.

        Returns:
            list: 중위 순회 결과(노드 데이터의 리스트)
        """
        if self.root:
            return self.root.inorder()
        else:
            return []

    def preorder(self) -> List[Any]:
        """
        트리의 전위 순회 결과를 리스트로 반환한다.

        Returns:
            list: 전위 순회 결과(노드 데이터의 리스트)
        """
        if self.root:
            return self.root.preorder()
        else:
            return []

    def postorder(self) -> List[Any]:
        """
        트리의 후위 순회 결과를 리스트로 반환한다.

        Returns:
            list: 후위 순회 결과(노드 데이터의 리스트)
        """
        if self.root:
            return self.root.postorder()
        else:
            return []
