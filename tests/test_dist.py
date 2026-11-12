# -*- coding: utf-8 -*-
import unittest

from qharness.dist import ShardRouter, hash_shard, Cluster, Node


class TestDist(unittest.TestCase):
    def test_hash_shard_stable(self):
        self.assertEqual(hash_shard("abc", 3), hash_shard("abc", 3))

    def test_router_stable(self):
        r = ShardRouter(["n1", "n2", "n3"])
        self.assertEqual(r.route("x"), r.route("x"))

    def test_cluster(self):
        nodes = [Node(id="b", role="brain"), Node(id="h", role="hand")]
        c = Cluster(nodes)
        self.assertEqual(c.summary()["brain_nodes"], 1)
        self.assertIsNotNone(c.hand_for("s"))


if __name__ == "__main__":
    unittest.main()
